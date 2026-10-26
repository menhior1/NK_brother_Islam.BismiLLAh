import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
const localized = z.object({ ka:z.string().default(''), ru:z.string().default(''), en:z.string().default('') });
const products = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/data/products' }),
  schema: z.object({
    title: localized,
    category: z.enum(['Round','Oval','Rectangular','Custom','Other']).default('Other'),
    description: localized,
    material: localized,
    finish: localized,
    dimensions: localized,
    coverImage: z.string().min(1),
    gallery: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    published: z.boolean().default(false),
    order: z.coerce.number().default(99),
    alt: localized
  })
});
export const collections = { products };
