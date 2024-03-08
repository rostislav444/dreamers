import {CategoryState} from "@/interfaces/Categories";
import {ProductPartsInterface} from "@/interfaces/Materials";
import {CameraInterface} from "@/interfaces/Product/Camera";


export interface ProductProps {
    product: ProductInterface,
    skuId?: string
}


export interface SkuImageInterface {
    image: string
}


export interface SkuInterface {
    id: number,
    images: SkuImageInterface[],
    code: string
    materials: { [key: number]: number };
}

export interface Model3dInterface {
    obj: string;
    mtl: string;
    cameras: CameraInterface[]
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
    images_by_sku: boolean
    model_3d: Model3dInterface
}
