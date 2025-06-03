import React, {useState} from "react";
import {Box} from "@chakra-ui/react";
import {CatalogueProductImages} from "@/components/App/Catalogue/ProductCard/Images";
import Link from "next/link";
import {ProductInterface} from "@/interfaces/Product";
import {MaterialsSet} from "@/components/App/Catalogue/ProductCard/MaterialsSet";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {CameraImageFromMaterials, setInitialMaterials} from "@/utils/Product/Materials";
import {UniversalMaterials} from "@/components/Shared/Materials/UniversalMaterials";
import { log } from "console";


interface Props {
    product: ProductInterface
}

const objectToMaterialsString = (obj: any) => {
    return 'materials_' + Object.values(obj).map((material: any) => `${material.partId}-${material.material}`).join('_');
};

export const ProductCard = ({product}: Props) => {
    const [selectedMaterials, setSelectedMaterials] = useState<SelectedMaterialsInterface>({
        ...setInitialMaterials(product.material_parts)
    });

    const images = product.camera ? CameraImageFromMaterials(product.camera.parts, selectedMaterials) : []
    const link = `/product/${product.code}/${objectToMaterialsString(selectedMaterials)}`


    return (
        <Box 
            bg="rgba(255, 255, 255, 0.5)"
            border="none"
            overflow="hidden"
            borderRadius="xl"
            transition="all 0.3s ease"
            _hover={{ 
                bg: "rgba(255, 255, 255, 0.8)"
            }}
        >
            <Link href={link}>
                <CatalogueProductImages images={images}/>
            </Link>
            <Box p="4">
                <Link href={link}>
                    <Box fontWeight="semibold" as="h4" lineHeight="tight" noOfLines={1} pb={2}>
                        {product.name}
                    </Box>
                </Link>
                <UniversalMaterials
                    parts={product.material_parts}
                    selectedMaterials={selectedMaterials}
                    setSelectedMaterials={setSelectedMaterials}
                    isCatalog={true}
                />
                <Box mt={3}>
                    <Box as="span" fontSize="lg" fontWeight="medium" color="brown.600">
                        {product.price} {"грн."}
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};
