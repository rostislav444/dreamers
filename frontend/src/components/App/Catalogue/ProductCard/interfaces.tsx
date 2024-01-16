export interface PartMaterial {
  id: number;
  color?: {
    id: number;
    name: string;
    hex: string;
  };
  material?: {
    id: number,
    name: string;
    image: string;
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
    sku: SkuInterface[];
  };
}

export interface SkuMaterialsResponse {
  [key: string]: number[];
}

export interface FilterMaterialsProps {
  parts: PartInterface[];
  skus: SkuInterface[];
  selectedMaterials: Record<string, number>
}
