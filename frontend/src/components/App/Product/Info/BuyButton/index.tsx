import {ProductInterface} from "@/interfaces/Product";
import {Box, Button, Text} from "@chakra-ui/react";
import {useCart} from "@/context/Cart";
import {useRouter} from "next/router";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {getThumbnailM} from "@/utils/Product/Materials";


interface ButButtonProps {
    product: ProductInterface
    selectedMaterials: SelectedMaterialsInterface
}

export const BuyButton = ({product, selectedMaterials}: ButButtonProps) => {
    const {addItem} = useCart()
    const router = useRouter();
    const partsSum = Object.entries(selectedMaterials).reduce((acc, [key, value]) => {
        return acc + product.customized_parts[key].material_groups[value.group].price
    }, product.price)

    const handleAddCartItem = () => {
        const currentPath = router.asPath
        const payload = {
            product: product.id,
            sku: 0,
            name: product.name,
            code: product.code,
            price: partsSum,
            qty: 1,
            images: getThumbnailM(product.model_3d[0].cameras[3].parts, selectedMaterials),
            materials: selectedMaterials,
            url: currentPath
        }
        addItem(payload)
        router.push('/order')
    }

    return <Box>
        <Text color={'brown.500'} fontSize={24} mt={8}>{partsSum} грн.</Text>
        <Button w={'100%'} mt={8} p={6} borderRadius='6px' onClick={handleAddCartItem}>Придбати</Button>
    </Box>
}