import {Box, Text} from "@chakra-ui/react";
import {ProductInterface} from "@/interfaces/Product";
import {ProductCharacteristics} from "@/components/App/Product/Info/Characteristic";
import {BuyButton} from "@/components/App/Product/Info/BuyButton";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {UniversalMaterials} from "@/components/Shared/Materials/UniversalMaterials";

interface ProductInfoProps {
    mobile: boolean
    product: ProductInterface
    selectedMaterials: SelectedMaterialsInterface
    setSelectedMaterials: any
}

export const ProductInfo = ({mobile, product, selectedMaterials, setSelectedMaterials}: ProductInfoProps) => {
    return <Box w='100%' pl={mobile ? 0 : 8} >
        <UniversalMaterials
            parts={product.material_parts}
            selectedMaterials={selectedMaterials}
            setSelectedMaterials={setSelectedMaterials}
            mobile={mobile}
        />
        <BuyButton product={product} selectedMaterials={selectedMaterials} />
        <ProductCharacteristics product={product} selectedMaterials={selectedMaterials}/>
        <InfoHeading mobile={mobile}>Опис</InfoHeading>
        <Text maxH='48' overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
    </Box>
}