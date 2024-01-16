export interface CategoryState {
  id: number;
  name: string;
  slug: string;
  image?: string,
}

export interface CategoryListProps {
  categories: CategoryState[];
}