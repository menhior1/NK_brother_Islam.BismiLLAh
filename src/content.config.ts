import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const products = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/data/products' }),
  schema: z.object({
    title: z.string().min(1),
    category: z.enum(['Round', 'Oval', 'Rectangular', 'Custom', 'Other']).default('Other'),
    description: z.string().default(''),
    material: z.string().default(''),
    finish: z.string().default(''),
    dimensions: z.string().default(''),
    coverImage: z.string().min(1),
    gallery: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    published: z.boolean().default(false),
    order: z.coerce.number().default(99),
    alt: z.string().default('')
  })
});

export const collections = { products };
