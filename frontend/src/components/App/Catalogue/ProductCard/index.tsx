import React, {useState} from "react";
import {Box} from "@chakra-ui/react";
import {CatalogueProductImages} from "@/components/App/Catalogue/ProductCard/Images";
import Link from "next/link";
import {ProductInterface} from "@/interfaces/Product";
import {MaterialsSet} from "@/components/App/Catalogue/ProductCard/MaterialsSet";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {CameraImageFromMaterials, setInitialMaterials} from "@/utils/Product/Materials";


interface Props {
    product: ProductInterface
}

const objectToMaterialsString = (obj: any) => {
    return 'materials_' + Object.entries(obj).map(([key, value]) => `${key}-${value}`).join('_');
};

export const ProductCard = ({product}: Props) => {
    const [selectedMaterials, setSelectedMaterials] = useState<SelectedMaterialsInterface>({
        ...setInitialMaterials(product.material_parts)
    });

    const images = product.camera ? CameraImageFromMaterials(product.camera.parts, selectedMaterials) : []
    const link = `/product/${product.code}/${objectToMaterialsString(selectedMaterials)}`

    return (
        <Box borderWidth="3px" borderColor={"brown.500"} overflow="hidden">
            <Link href={link}>
                <CatalogueProductImages images={images}/>
            </Link>
            <Box p="4">
                <Link href={link}>
                    <Box fontWeight="semibold" as="h4" lineHeight="tight" noOfLines={1} pb={2}>
                        {product.name}
                    </Box>
                </Link>
                <MaterialsSet material_parts={product.material_parts} setSelectedMaterial={setSelectedMaterials}
                              selectedMaterial={selectedMaterials}/>
                <Box>
                    <Box as="span" fontSize="l">
                        {product.price} {"грн."}
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};
