import {CategoryState} from "@/interfaces/Categories";
import {ProductPartsInterface} from "@/interfaces/Materials";

export interface SkuImageInterface {
    image: string
}


export interface SkuInterface {
    id: number,
    images: SkuImageInterface[],
    code: string
    materials: { [key: number]: number };
}


export interface ProductInterface {
    id: number;
    name: string;
    description: 'string',
    code: string;
    price: number;
    sku: SkuInterface[];
    categories: CategoryState[]
    parts: ProductPartsInterface[];
    width: number;
    height: number;
    depth: number;
}
