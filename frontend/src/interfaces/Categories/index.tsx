export interface CategoryState {
  id: number;
  name: string;
  slug: string;
  image?: string,
}

export interface RecursiveCategoryInterface {
    id: number;
    name: string;
    slug: string;
    children: RecursiveCategoryInterface[] | null;
}

export interface CategoryListProps {
  categories: CategoryState[];
}