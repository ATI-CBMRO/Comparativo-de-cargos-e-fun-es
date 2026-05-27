import { z } from "zod";
import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";
import {
  getAllStates,
  getDashboardStats,
  getFilteredData,
  getPositionsByOperationalCommandIds,
  getPositionsByTechnicalDirectorateIds,
  getPositionCategories,
  getPositionsByCategory,
  getStateDetails,
} from "./db";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query((opts) => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
  }),

  // ─── States ──────────────────────────────────────────────────────────────
  states: router({
    list: publicProcedure.query(async () => {
      return getAllStates();
    }),

    details: publicProcedure
      .input(z.object({ sigla: z.string().length(2) }))
      .query(async ({ input }) => {
        return getStateDetails(input.sigla);
      }),
  }),

  // ─── Dashboard Stats ──────────────────────────────────────────────────────
  dashboard: router({
    stats: publicProcedure.query(async () => {
      return getDashboardStats();
    }),
  }),

  // ─── Filtered Data ────────────────────────────────────────────────────────
  data: router({
    allStates: publicProcedure.query(async () => {
      return getAllStates();
    }),

    filtered: publicProcedure
      .input(
        z.object({
          siglas: z.array(z.string()).optional(),
          detailLevel: z
            .array(z.enum(["detalhado", "moderado", "basico"]))
            .optional(),
          orgType: z.enum(["all", "operational", "technical"]).optional(),
          search: z.string().optional(),
        })
      )
      .query(async ({ input }) => {
        const results = await getFilteredData({
          siglas: input.siglas,
          detailLevel: input.detailLevel,
          search: input.search,
        });

        // Filter by org type
        if (input.orgType === "operational") {
          return results.map((r) => ({ ...r, technicalDirectorate: null }));
        }
        if (input.orgType === "technical") {
          return results.map((r) => ({ ...r, operationalCommand: null }));
        }
        return results;
      }),

    // Tipos de categorias de cargos disponíveis
    positionTypes: publicProcedure.query(async () => {
      return getPositionCategories();
    }),

    // Comparativo por categoria de cargo
    comparePositions: publicProcedure
      .input(
        z.object({
          category: z.string().min(1),
          siglas: z.array(z.string().length(2)).optional(),
        })
      )
      .query(async ({ input }) => {
        const results = await getPositionsByCategory(input.category);
        // Filter by states if provided
        if (input.siglas && input.siglas.length > 0) {
          return results.filter(
            (r) => r.state && input.siglas!.includes(r.state.sigla)
          );
        }
        return results;
      }),

    // Comparativo com cargos e funções completos
    comparative: publicProcedure
      .input(
        z.object({
          siglas: z.array(z.string().length(2)).min(1).max(5),
        })
      )
      .query(async ({ input }) => {
        const results = await getFilteredData({ siglas: input.siglas });

        // Collect IDs
        const ocIds = results
          .map((r) => r.operationalCommand?.id)
          .filter((id): id is number => id !== undefined && id !== null);
        const tdIds = results
          .map((r) => r.technicalDirectorate?.id)
          .filter((id): id is number => id !== undefined && id !== null);

        // Fetch all positions in two queries
        const [ocPositions, tdPositions] = await Promise.all([
          getPositionsByOperationalCommandIds(ocIds),
          getPositionsByTechnicalDirectorateIds(tdIds),
        ]);

        // Attach positions to each state result
        return results.map((r) => ({
          ...r,
          ocPositions: r.operationalCommand
            ? ocPositions.filter((p) => p.operationalCommandId === r.operationalCommand!.id)
            : [],
          tdPositions: r.technicalDirectorate
            ? tdPositions.filter((p) => p.technicalDirectorateId === r.technicalDirectorate!.id)
            : [],
        }));
      }),
  }),
});

export type AppRouter = typeof appRouter;
