# Portfolio link (when ready)

Add a card in `my-website/src/lib/projects.ts`:

```ts
{
  id: 'water-bucket-puzzle',
  title: 'Water Bucket Puzzle',
  description: 'Classic pouring puzzle with 8L, 5L, and 3L buckets — reach exactly 4 liters in the fewest moves.',
  technologies: ['Python', 'FastAPI'],
  status: 'planned',
  category: 'web',
  demoUrl: process.env.NEXT_PUBLIC_WATER_BUCKET_PUZZLE_DEMO_URL ?? 'http://localhost:3007',
  github: 'https://github.com/emmarthur/water-bucket-puzzle',
}
```

Deploy separately; portfolio links out only.
