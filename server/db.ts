import { and, asc, eq, inArray, like, or } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { InsertUser, operationalCommands, positions, states, technicalDirectorates, users } from "../drizzle/schema";
import { ENV } from "./_core/env";

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) throw new Error("User openId is required for upsert");
  const db = await getDb();
  if (!db) return;

  try {
    const values: InsertUser = { openId: user.openId };
    const updateSet: Record<string, unknown> = {};
    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];
    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };
    textFields.forEach(assignNullable);
    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = "admin";
      updateSet.role = "admin";
    }
    if (!values.lastSignedIn) values.lastSignedIn = new Date();
    if (Object.keys(updateSet).length === 0) updateSet.lastSignedIn = new Date();
    await db.insert(users).values(values).onDuplicateKeyUpdate({ set: updateSet });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) return undefined;
  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ─── States ────────────────────────────────────────────────────────────────

export async function getAllStates() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(states).orderBy(states.name);
}

export async function getStateBySigna(sigla: string) {
  const db = await getDb();
  if (!db) return undefined;
  const result = await db.select().from(states).where(eq(states.sigla, sigla)).limit(1);
  return result[0] ?? undefined;
}

// ─── Operational Commands ──────────────────────────────────────────────────

export async function getAllOperationalCommands() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(operationalCommands);
}

export async function getOperationalCommandsByState(stateId: number) {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(operationalCommands).where(eq(operationalCommands.stateId, stateId));
}

// ─── Technical Directorates ────────────────────────────────────────────────

export async function getAllTechnicalDirectorates() {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(technicalDirectorates);
}

export async function getTechnicalDirectoratesByState(stateId: number) {
  const db = await getDb();
  if (!db) return [];
  return db.select().from(technicalDirectorates).where(eq(technicalDirectorates.stateId, stateId));
}

// ─── Combined Query with Filters ──────────────────────────────────────────

export type FilterParams = {
  siglas?: string[];
  detailLevel?: ("detalhado" | "moderado" | "basico")[];
  search?: string;
};

export async function getFilteredData(params: FilterParams) {
  const db = await getDb();
  if (!db) return [];

  // Get matching states
  let stateQuery = db.select().from(states);
  if (params.siglas && params.siglas.length > 0) {
    stateQuery = stateQuery.where(inArray(states.sigla, params.siglas)) as typeof stateQuery;
  }
  const matchedStates = await stateQuery.orderBy(states.name);

  if (matchedStates.length === 0) return [];

  const stateIds = matchedStates.map((s) => s.id);

  // Get operational commands
  let ocConditions: ReturnType<typeof and>[] = [];
  const ocStateCondition = inArray(operationalCommands.stateId, stateIds);
  if (params.detailLevel && params.detailLevel.length > 0) {
    ocConditions.push(and(ocStateCondition, inArray(operationalCommands.detailLevel, params.detailLevel))!);
  } else {
    ocConditions.push(ocStateCondition as any);
  }

  let ocQuery = db.select().from(operationalCommands).where(ocConditions[0]);
  if (params.search) {
    const term = `%${params.search}%`;
    ocQuery = db
      .select()
      .from(operationalCommands)
      .where(
        and(
          ocConditions[0],
          or(
            like(operationalCommands.nomenclature, term),
            like(operationalCommands.attributions, term),
            like(operationalCommands.subdivisions, term)
          )
        )
      ) as typeof ocQuery;
  }
  const ocs = await ocQuery;

  // Get technical directorates
  let tdConditions: ReturnType<typeof and>[] = [];
  const tdStateCondition = inArray(technicalDirectorates.stateId, stateIds);
  if (params.detailLevel && params.detailLevel.length > 0) {
    tdConditions.push(and(tdStateCondition, inArray(technicalDirectorates.detailLevel, params.detailLevel))!);
  } else {
    tdConditions.push(tdStateCondition as any);
  }

  let tdQuery = db.select().from(technicalDirectorates).where(tdConditions[0]);
  if (params.search) {
    const term = `%${params.search}%`;
    tdQuery = db
      .select()
      .from(technicalDirectorates)
      .where(
        and(
          tdConditions[0],
          or(
            like(technicalDirectorates.nomenclature, term),
            like(technicalDirectorates.attributions, term),
            like(technicalDirectorates.subdivisions, term)
          )
        )
      ) as typeof tdQuery;
  }
  const tds = await tdQuery;

  // Merge into state-keyed result
  return matchedStates.map((state) => ({
    state,
    operationalCommand: ocs.find((oc) => oc.stateId === state.id) ?? null,
    technicalDirectorate: tds.find((td) => td.stateId === state.id) ?? null,
  }));
}

// ─── Positions ────────────────────────────────────────────────────────────

export async function getPositionsByOperationalCommand(operationalCommandId: number) {
  const db = await getDb();
  if (!db) return [];
  return db
    .select()
    .from(positions)
    .where(eq(positions.operationalCommandId, operationalCommandId))
    .orderBy(asc(positions.sortOrder));
}

export async function getPositionsByTechnicalDirectorate(technicalDirectorateId: number) {
  const db = await getDb();
  if (!db) return [];
  return db
    .select()
    .from(positions)
    .where(eq(positions.technicalDirectorateId, technicalDirectorateId))
    .orderBy(asc(positions.sortOrder));
}

export async function getPositionsByOperationalCommandIds(ids: number[]) {
  const db = await getDb();
  if (!db || ids.length === 0) return [];
  return db
    .select()
    .from(positions)
    .where(inArray(positions.operationalCommandId, ids))
    .orderBy(asc(positions.sortOrder));
}

export async function getPositionsByTechnicalDirectorateIds(ids: number[]) {
  const db = await getDb();
  if (!db || ids.length === 0) return [];
  return db
    .select()
    .from(positions)
    .where(inArray(positions.technicalDirectorateId, ids))
    .orderBy(asc(positions.sortOrder));
}

// ─── State Details (with positions) ───────────────────────────────────────

export async function getStateDetails(sigla: string) {
  const db = await getDb();
  if (!db) return null;

  const stateResult = await db.select().from(states).where(eq(states.sigla, sigla)).limit(1);
  if (!stateResult[0]) return null;

  const state = stateResult[0];
  const [oc] = await db
    .select()
    .from(operationalCommands)
    .where(eq(operationalCommands.stateId, state.id))
    .limit(1);
  const [td] = await db
    .select()
    .from(technicalDirectorates)
    .where(eq(technicalDirectorates.stateId, state.id))
    .limit(1);

  const ocPositions = oc ? await getPositionsByOperationalCommand(oc.id) : [];
  const tdPositions = td ? await getPositionsByTechnicalDirectorate(td.id) : [];

  return {
    state,
    operationalCommand: oc ?? null,
    technicalDirectorate: td ?? null,
    ocPositions,
    tdPositions,
  };
}

export async function getDashboardStats() {
  const db = await getDb();
  if (!db) return { totalStates: 0, detalhado: 0, moderado: 0, basico: 0, byRegion: [] };

  const allStates = await db.select().from(states);
  const allOcs = await db.select().from(operationalCommands);
  const allTds = await db.select().from(technicalDirectorates);

  const countByLevel = (items: { detailLevel: string }[]) => ({
    detalhado: items.filter((i) => i.detailLevel === "detalhado").length,
    moderado: items.filter((i) => i.detailLevel === "moderado").length,
    basico: items.filter((i) => i.detailLevel === "basico").length,
  });

  const regions = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"] as const;
  const byRegion = regions.map((region) => ({
    region,
    count: allStates.filter((s) => s.region === region).length,
  }));

  return {
    totalStates: allStates.length,
    operationalCommands: countByLevel(allOcs),
    technicalDirectorates: countByLevel(allTds),
    byRegion,
  };
}
