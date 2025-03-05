export interface PartMaterial {
  id: number;
  material?: {
    id: number,
    name: string;
    image: string;
    color?: {
      id: number;
      name: string;
      hex: string;
    };
  }
}


export interface PartInterface {
  id: number;
  name: string;
  materials: PartMaterial[];
}

export interface SkuMaterials {
  [key: string]: number;
}

export interface SkuInterface {
  id: number;
  code: string;
  images: string[];
  materials: SkuMaterials;
}


export interface ProductCardProps {
  product: {
    id: number;
    name: string;
    code: string;
    price: number;
    parts: PartInterface[];
    part_images: string[];
    sku: SkuInterface[];
  };
  part_images: string[];
}

export interface SkuMaterialsResponse {
  [key: string]: number[];
}

export interface FilterMaterialsProps {
  parts: PartInterface[];
  skus: SkuInterface[];
  selectedMaterials: Record<string, number>
}
