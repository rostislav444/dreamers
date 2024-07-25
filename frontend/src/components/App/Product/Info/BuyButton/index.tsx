import {ProductInterface} from "@/interfaces/Product";
import {Box, Button, Text} from "@chakra-ui/react";
import {useCart} from "@/context/Cart";
import {useRouter} from "next/router";


interface ButButtonProps {
    product: ProductInterface
}

export const ButButton = ({product}: ButButtonProps) => {
    const router = useRouter();
    const {addItem} = useCart()

    const handleAddCartItem = () => {
        const payload = {
            product: product.id,
            sku: 0,
            name: product.name,
            code: product.code,
            price: product.price,
            qty: 1,
            image: 'image',
            material: {
                color: ''
            }
        }
        addItem(payload)
        router.push('/order')
    }

    return <Box>
        <Text color={'brown.500'} fontSize={24} mt={8}>{product.price} грн.</Text>
        <Button w={'100%'} mt={8} p={6} onClick={handleAddCartItem}>Придбати</Button>
    </Box>
}