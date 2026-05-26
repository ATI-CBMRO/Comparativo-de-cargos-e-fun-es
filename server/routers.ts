import { z } from "zod";
import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";
import {
  getAllStates,
  getDashboardStats,
  getFilteredData,
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
  }),
});

export type AppRouter = typeof appRouter;
