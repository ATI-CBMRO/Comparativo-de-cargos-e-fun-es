import { describe, expect, it, vi } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

// vi.mock is hoisted to the top of the file, so we cannot reference variables
// defined outside the factory. All mock data must be defined inside the factory.
vi.mock("./db", () => {
  const ocPositions = [
    {
      id: 1,
      operationalCommandId: 1,
      technicalDirectorateId: null,
      title: "Diretor de Planejamento Operacional",
      acronym: "DPO",
      rank: "Coronel BM",
      subordinateTo: "Comandante Geral",
      subordinates: "Coordenadoria de Operações; Coordenadoria de Doutrina",
      attributions: "Planejar e coordenar as atividades operacionais; Assessorar o Comandante",
      sortOrder: 1,
    },
  ];

  const tdPositions = [
    {
      id: 2,
      operationalCommandId: null,
      technicalDirectorateId: 1,
      title: "Diretor de Atividades Técnicas",
      acronym: "DAT",
      rank: "Coronel BM",
      subordinateTo: "Comandante Geral",
      subordinates: "Seção de Estudos Técnicos; Seção de Planejamento Técnico",
      attributions: "Planejar e coordenar as atividades técnicas; Normatizar procedimentos",
      sortOrder: 1,
    },
  ];

  const stateRO = {
    id: 1,
    sigla: "RO",
    name: "Rondônia",
    region: "Norte",
    corporationName: "Corpo de Bombeiros Militar de Rondônia",
    legislationDocuments: "Minuta de Lei de Organização Básica do CBMRO",
  };

  const ocRO = {
    id: 1,
    stateId: 1,
    nomenclature: "Diretoria de Planejamento Operacional",
    acronym: "DPO",
    subdivisions: "Coordenadoria de Operações",
    attributions: "Planejar atividades operacionais",
    detailLevel: "detalhado",
    legalBasis: "Minuta de Lei",
    notes: null,
  };

  const tdRO = {
    id: 1,
    stateId: 1,
    nomenclature: "Comando de Operações Técnicas",
    acronym: "COT",
    subdivisions: "Seção de Estudos Técnicos",
    attributions: "Planejar atividades técnicas",
    detailLevel: "detalhado",
    legalBasis: "Minuta de Lei",
    notes: null,
  };

  return {
    getAllStates: vi.fn().mockResolvedValue([
      stateRO,
      {
        id: 2,
        sigla: "DF",
        name: "Distrito Federal",
        region: "Centro-Oeste",
        corporationName: "Corpo de Bombeiros Militar do Distrito Federal",
        legislationDocuments: "Regimento Interno do CBMDF",
      },
    ]),
    getDashboardStats: vi.fn().mockResolvedValue({
      totalStates: 19,
      operationalCommands: { detalhado: 9, moderado: 7, basico: 3 },
      technicalDirectorates: { detalhado: 10, moderado: 8, basico: 1 },
      byRegion: [
        { region: "Norte", count: 3 },
        { region: "Nordeste", count: 7 },
        { region: "Centro-Oeste", count: 3 },
        { region: "Sudeste", count: 3 },
        { region: "Sul", count: 3 },
      ],
    }),
    getFilteredData: vi.fn().mockResolvedValue([
      {
        state: stateRO,
        operationalCommand: ocRO,
        technicalDirectorate: tdRO,
      },
    ]),
    getStateDetails: vi.fn().mockResolvedValue({
      state: stateRO,
      operationalCommand: ocRO,
      technicalDirectorate: tdRO,
      ocPositions,
      tdPositions,
    }),
    getPositionsByOperationalCommandIds: vi.fn().mockResolvedValue(ocPositions),
    getPositionsByTechnicalDirectorateIds: vi.fn().mockResolvedValue(tdPositions),
    upsertUser: vi.fn(),
    getUserByOpenId: vi.fn(),
  };
});

function createPublicContext(): TrpcContext {
  return {
    user: null,
    req: { protocol: "https", headers: {} } as TrpcContext["req"],
    res: { clearCookie: vi.fn() } as unknown as TrpcContext["res"],
  };
}

describe("states.list", () => {
  it("returns list of states", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.states.list();
    expect(result).toHaveLength(2);
    expect(result[0].sigla).toBe("RO");
    expect(result[1].sigla).toBe("DF");
  });
});

describe("states.details", () => {
  it("returns state details for a valid sigla", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.states.details({ sigla: "RO" });
    expect(result).not.toBeNull();
    expect(result?.state.sigla).toBe("RO");
    expect(result?.operationalCommand).not.toBeNull();
    expect(result?.technicalDirectorate).not.toBeNull();
  });

  it("returns ocPositions and tdPositions in state details", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.states.details({ sigla: "RO" });
    expect(result).not.toBeNull();
    expect(result).toHaveProperty("ocPositions");
    expect(result).toHaveProperty("tdPositions");
    expect(Array.isArray((result as any).ocPositions)).toBe(true);
    expect(Array.isArray((result as any).tdPositions)).toBe(true);
    expect((result as any).ocPositions[0].title).toBe("Diretor de Planejamento Operacional");
    expect((result as any).tdPositions[0].title).toBe("Diretor de Atividades Técnicas");
  });

  it("validates sigla length", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    await expect(caller.states.details({ sigla: "INVALID" })).rejects.toThrow();
  });
});

describe("dashboard.stats", () => {
  it("returns dashboard statistics", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.dashboard.stats();
    expect(result.totalStates).toBe(19);
    expect(result.operationalCommands?.detalhado).toBe(9);
    expect(result.technicalDirectorates?.detalhado).toBe(10);
    expect(result.byRegion).toHaveLength(5);
  });
});

describe("data.filtered", () => {
  it("returns filtered results with no filters", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({});
    expect(result).toHaveLength(1);
    expect(result[0].state.sigla).toBe("RO");
  });

  it("filters by orgType operational - hides technical directorate", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({ orgType: "operational" });
    expect(result[0].technicalDirectorate).toBeNull();
    expect(result[0].operationalCommand).not.toBeNull();
  });

  it("filters by orgType technical - hides operational command", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({ orgType: "technical" });
    expect(result[0].operationalCommand).toBeNull();
    expect(result[0].technicalDirectorate).not.toBeNull();
  });

  it("accepts siglas filter", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({ siglas: ["RO", "DF"] });
    expect(result).toBeDefined();
  });

  it("accepts detailLevel filter", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({ detailLevel: ["detalhado"] });
    expect(result).toBeDefined();
  });

  it("accepts search filter", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.filtered({ search: "operacional" });
    expect(result).toBeDefined();
  });
});

describe("data.comparative", () => {
  it("returns comparative data with positions for selected states", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.comparative({ siglas: ["RO"] });
    expect(result).toHaveLength(1);
    expect(result[0].state.sigla).toBe("RO");
    expect(result[0].ocPositions).toBeDefined();
    expect(result[0].tdPositions).toBeDefined();
  });

  it("includes oc positions with title and attributions", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.comparative({ siglas: ["RO"] });
    const ocPos = result[0].ocPositions;
    expect(Array.isArray(ocPos)).toBe(true);
    expect(ocPos.length).toBeGreaterThan(0);
    expect(ocPos[0]).toHaveProperty("title");
    expect(ocPos[0]).toHaveProperty("attributions");
    expect(ocPos[0].title).toBe("Diretor de Planejamento Operacional");
  });

  it("includes td positions with title and subordinateTo", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const result = await caller.data.comparative({ siglas: ["RO"] });
    const tdPos = result[0].tdPositions;
    expect(Array.isArray(tdPos)).toBe(true);
    expect(tdPos.length).toBeGreaterThan(0);
    expect(tdPos[0]).toHaveProperty("title");
    expect(tdPos[0]).toHaveProperty("subordinateTo");
    expect(tdPos[0].title).toBe("Diretor de Atividades Técnicas");
  });

  it("rejects more than 5 states", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    await expect(
      caller.data.comparative({ siglas: ["RO", "DF", "AL", "CE", "MA", "PA"] })
    ).rejects.toThrow();
  });

  it("rejects empty siglas array", async () => {
    const caller = appRouter.createCaller(createPublicContext());
    await expect(caller.data.comparative({ siglas: [] })).rejects.toThrow();
  });
});
