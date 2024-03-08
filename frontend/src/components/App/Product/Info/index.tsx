import {Box, Heading, Text} from "@chakra-ui/react";
import {ProductMaterials} from "src/components/App/Product/Info/Materials";
import {ProductInterface} from "@/interfaces/Product";
import {selectedMaterialsInterface} from "@/components/App/Product";
import {ProductCharacteristics} from "@/components/App/Product/Info/Characteristic";
import {ButButton} from "@/components/App/Product/Info/BuyButton";
import {InfoHeading} from "@/components/Shared/Typogrphy";

interface ProductInfoProps {
    mobile: boolean
    product: ProductInterface
    selectedMaterials: selectedMaterialsInterface
    setSelectedMaterials: any
}

export const ProductInfo = ({mobile, product, selectedMaterials, setSelectedMaterials}: ProductInfoProps) => {
    return <Box>
        <Heading mb={mobile ? 4 : 8}>{product.name}</Heading>
        <ProductMaterials
            parts={product.parts}
            materials={selectedMaterials}
            setSelectedMaterials={setSelectedMaterials}
        />
        <ButButton product={product} selectedMaterials={selectedMaterials}/>
        <ProductCharacteristics product={product} selectedMaterials={selectedMaterials}/>
        <InfoHeading mobile={mobile}>Опис</InfoHeading>
        <Text maxH='48' overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
    </Box>
}