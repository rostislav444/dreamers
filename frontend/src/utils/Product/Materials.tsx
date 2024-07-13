import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {ProductPart} from "@/interfaces/Product/Parts";
import {CameraProductPartInterface} from "@/interfaces/Product/Camera";

function getRandomInt(max: number) {
  return Math.floor(Math.random() * max);
}


export const setInitialMaterials = (material_parts: ProductPart[]) => {
    const initialMaterials: SelectedMaterialsInterface = {};

    material_parts.forEach(part => {
        const length =  part.material_groups[0].materials.length
        const randomIndex = getRandomInt(length)
        initialMaterials[part.id] = part.material_groups[0].materials[randomIndex].id;
    });
    return initialMaterials;
}


export const CameraImageFromMaterials = (parts: CameraProductPartInterface[], selectedMaterials: SelectedMaterialsInterface) => {
    return parts.map(part => {
        const partId = part.part.id
        return part.materials.find(material => material.material == selectedMaterials[partId])?.image || ''
    })
}