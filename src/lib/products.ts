import { getCollection } from 'astro:content';

export async function publishedProducts() {
  return (await getCollection('products'))
    .filter(({ data }) => data.published)
    .sort((a, b) => a.data.order - b.data.order || a.data.title.localeCompare(b.data.title));
}
