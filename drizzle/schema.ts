import {
  int,
  mysqlEnum,
  mysqlTable,
  text,
  timestamp,
  varchar,
} from "drizzle-orm/mysql-core";

export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// Tabela de estados
export const states = mysqlTable("states", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  sigla: varchar("sigla", { length: 2 }).notNull().unique(),
  region: mysqlEnum("region", ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]).notNull(),
  corporationName: varchar("corporationName", { length: 200 }).notNull(),
  legislationDocuments: text("legislationDocuments"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type State = typeof states.$inferSelect;
export type InsertState = typeof states.$inferInsert;

// Tabela de Comandos Operacionais
export const operationalCommands = mysqlTable("operational_commands", {
  id: int("id").autoincrement().primaryKey(),
  stateId: int("stateId").notNull(),
  nomenclature: varchar("nomenclature", { length: 300 }).notNull(),
  acronym: varchar("acronym", { length: 50 }),
  subdivisions: text("subdivisions"),
  attributions: text("attributions"),
  detailLevel: mysqlEnum("detailLevel", ["detalhado", "moderado", "basico"]).notNull(),
  legalBasis: varchar("legalBasis", { length: 300 }),
  notes: text("notes"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type OperationalCommand = typeof operationalCommands.$inferSelect;
export type InsertOperationalCommand = typeof operationalCommands.$inferInsert;

// Tabela de Diretorias de Atividades Técnicas
export const technicalDirectorates = mysqlTable("technical_directorates", {
  id: int("id").autoincrement().primaryKey(),
  stateId: int("stateId").notNull(),
  nomenclature: varchar("nomenclature", { length: 300 }).notNull(),
  acronym: varchar("acronym", { length: 50 }),
  subdivisions: text("subdivisions"),
  attributions: text("attributions"),
  detailLevel: mysqlEnum("detailLevel", ["detalhado", "moderado", "basico"]).notNull(),
  legalBasis: varchar("legalBasis", { length: 300 }),
  notes: text("notes"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type TechnicalDirectorate = typeof technicalDirectorates.$inferSelect;
export type InsertTechnicalDirectorate = typeof technicalDirectorates.$inferInsert;
