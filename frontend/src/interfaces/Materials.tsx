interface Color {
    id: number;
    name: string;
    hex: string;
    ral: string;
    rgb: [number, number, number];
}

interface Material {
    id: number,
    name: string
}


interface MaterialData {
    id: number;
    color?: Color;
    material?: Material;
    sub_group?: string;
}


export interface SubGroupsInterface {
    name: string
}

export interface MaterialGroupsInterface {
    id: number,
    type: string,
    materials: MaterialData[],
    sub_groups: SubGroupsInterface[]
}


export interface ProductPartsInterface {
    id: number,
    name: string,
    material_groups: MaterialGroupsInterface[]
}