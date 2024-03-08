import {ProductProps, SkuInterface} from "@/interfaces/Product";
import {useState} from "react";
import {chooseInitialMaterials, findSkuWithMaterialsSet} from "./utils";
import {ProductGallery} from "@/components/App/Product/Galery";
import {ProductMaterials} from "src/components/App/Product/Info/Materials";
import {Box, Button, Flex, Heading, Text, useMediaQuery} from "@chakra-ui/react";
import {ProductInfo} from "@/components/App/Product/Info";

export interface selectedMaterialsInterface {
    [key: number]: number
}


export const ProductComponent = ({product, skuId}: ProductProps) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const initialMaterials = chooseInitialMaterials(product.parts)
    const [selectedMaterials, setSelectedMaterials] = useState<selectedMaterialsInterface>(initialMaterials)

    // const selectedSku = product.images_by_sku ? findSkuWithMaterialsSet(initialMaterials, product.sku) : null

    return <Flex mb='2' flexDir={mobile ? 'column' : 'row'}>
        <ProductGallery mobile={mobile} product={product} selectedMaterials={selectedMaterials}/>
        <ProductInfo mobile={mobile} product={product} selectedMaterials={selectedMaterials} setSelectedMaterials={setSelectedMaterials}/>
    </Flex>
}