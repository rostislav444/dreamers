import {Box, Heading, Text} from "@chakra-ui/react";
import {ProductMaterials} from "src/components/App/Product/Info/Materials";
import {ProductInterface} from "@/interfaces/Product";
import {ProductCharacteristics} from "@/components/App/Product/Info/Characteristic";
import {ButButton} from "@/components/App/Product/Info/BuyButton";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";

interface ProductInfoProps {
    mobile: boolean
    product: ProductInterface
    selectedMaterials: SelectedMaterialsInterface
    setSelectedMaterials: any
}

export const ProductInfo = ({mobile, product, selectedMaterials, setSelectedMaterials}: ProductInfoProps) => {
    return <Box w='100%' pl={mobile ? 0 : 8} >
        <ProductMaterials
            parts={product.material_parts}
            selectedMaterials={selectedMaterials}
            setSelectedMaterials={setSelectedMaterials}
        />
        <ButButton product={product} selectedMaterials={selectedMaterials} />
        <ProductCharacteristics product={product} selectedMaterials={selectedMaterials}/>
        <InfoHeading mobile={mobile}>Опис</InfoHeading>
        <Text maxH='48' overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
    </Box>
}