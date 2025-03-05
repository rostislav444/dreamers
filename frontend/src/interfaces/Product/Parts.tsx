export interface ColorMaterial {
  id: number;
  name: string;
  hex: string;
  ral: string;
  rgb: number[];
}

export interface Material {
  name: string;
  id: number;
  color: ColorMaterial;
  material: any;
  sub_group: any;
}

export interface MaterialGroup {
  id: number;
  type: string;
  name: string;
  sub_groups: any[];
  materials: Material[];
}

export interface ProductPart {
  id: number;
  name: string;
  blender_name: string;
  material_groups: MaterialGroup[];
}