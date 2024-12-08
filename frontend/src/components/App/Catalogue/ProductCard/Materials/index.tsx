import {Box, Flex, Grid, Text, useMediaQuery} from "@chakra-ui/react";
import React, {useEffect, useRef, useState} from "react";
import {
    FilterMaterialsProps,
    PartInterface,
    ProductCardProps,
    SkuInterface,
    SkuMaterialsResponse
} from "@/components/App/Catalogue/ProductCard/interfaces";
import {BASE_URL, MEDIA_LOCAL} from "@/local";

interface ProductCardMaterialProps extends ProductCardProps {
    setSelectedSku: React.Dispatch<React.SetStateAction<number | null>>;
}

interface filterMaterialsResponse {
    newFilteredParts: PartInterface[],
    bestFitIndex: number
}

const getSkusMaterials = (skus: SkuInterface[], selectedMaterials: Record<string, number>): SkuMaterialsResponse => {
    const selectedMaterialKeys = Object.keys(selectedMaterials);

    return skus.reduce((result, sku) => {
        const hasSelectedMaterials = selectedMaterialKeys.every((key) => sku.materials[key] === selectedMaterials[key]);

        if (hasSelectedMaterials) {
            Object.entries(sku.materials).forEach(([key, materialId]) => {
                result[key] = Array.from(new Set([...(result[key] || []), materialId]));
            });
        }

        return result;
    }, {} as SkuMaterialsResponse);
};

const getBestFitSku = (selectedMaterials: any, skus: any) => {
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

const filterMaterials = ({parts, skus, selectedMaterials = {}}: FilterMaterialsProps): filterMaterialsResponse => {
    const skuMaterials = getSkusMaterials(skus, selectedMaterials);

    const newFilteredParts = parts.map((part) => {
        const filteredMaterials = part.materials.filter((material) => skuMaterials[part.id].includes(material.id));
        return {...part, materials: filteredMaterials};
    });

    const bestFitIndex = getBestFitSku(selectedMaterials, skus)

    return {bestFitIndex, newFilteredParts}
};

export const ProductCardMaterial = ({product, setSelectedSku}: ProductCardMaterialProps) => {
    // Filter out parts without materials at initialization
    const validParts = product.parts.filter(part => part.materials.length >= 1 && part.materials.length > 1);
    const productParts = useRef(validParts);

    const [selectedMaterials, setSelectedMaterials] = useState<Record<string, number>>({});
    const [filteredParts, setFilteredParts] = useState<PartInterface[]>([]);

    useEffect(() => {
        const {newFilteredParts, bestFitIndex} = filterMaterials(
            {parts: productParts.current, skus: product.sku, selectedMaterials});
        setFilteredParts(newFilteredParts);
        setSelectedSku(bestFitIndex)
    }, [selectedMaterials, product.sku, setSelectedSku]);

    const handleSelectMaterial = (partId: number, materialId: number) => {
        const newSelectedMaterials = {...selectedMaterials};

        if (newSelectedMaterials[partId] === materialId) {
            delete newSelectedMaterials[partId];
        } else {
            newSelectedMaterials[partId] = materialId;
        }

        setSelectedMaterials(newSelectedMaterials);
    };

    if (validParts.length === 0) {
        return null;
    }

    return (
        <Box mb={2}>
            {validParts.map((part) => (
                part.materials.length > 0 && (
                    <Box key={part.id}>
                        <Text as="span" mt={2}>
                            {part.name}
                        </Text>
                        <Grid mt={2} gridTemplateColumns={"repeat(auto-fill, 40px)"}
                              gridTemplateRows={"repeat(auto-fill, 40px)"} gap={1}>
                            {part.materials.map((material) => (
                                <Flex
                                    key={material.id}
                                    justifyContent="center"
                                    alignItems="center"
                                    onClick={() => handleSelectMaterial(part.id, material.id)}
                                    borderWidth={2}
                                    borderColor={selectedMaterials[part.id] === material.id ? "brown" : "transparent"}
                                >
                                    {material.color && <Box w={8} h={8} backgroundColor={material.color.hex}/>}
                                    {material.material &&
                                        <Box w={8} h={8} backgroundSize="cover" backgroundImage={MEDIA_LOCAL ? BASE_URL + material.material.image : material.material.image}/>}
                                </Flex>
                            ))}
                        </Grid>
                    </Box>
                )
            ))}
        </Box>
    );
};