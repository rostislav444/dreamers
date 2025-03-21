export interface CategoryState {
    description?: string;
    id: number;
    name: string;
    slug: string;
    image: string[]
}

export interface RecursiveCategoryInterface {
    id: number;
    name: string;
    slug: string;
    children: RecursiveCategoryInterface[] | null;
    image: string[]
}

export interface CategoryListProps {
    categories: CategoryState[];
}