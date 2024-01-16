export const getBestFitSku = (selectedMaterials: any, skus: any) => {
    let indexes: number[] = Array(skus.length).fill(0);

    for (let i = 0; i < skus.length; i++) {
        const sku = skus[i];
        for (const key of Object.keys(selectedMaterials)) {
            if (sku.materials[key] === selectedMaterials[key]) {
                indexes[i] += 1;
            }
        }
    }

    const maxIndex = indexes.indexOf(Math.max(...indexes));
    return maxIndex;
};