import {CartIcon} from "@/components/Shared/Icons/Cart";
import {Badge, Box} from "@chakra-ui/react";
import React from "react";
import {useCart} from "@/context/Cart";
import Link from "next/link";


export const CartCounter = () => {
    const {totalQty} = useCart();

    return <Link href={'/order'} >
        <Box position='relative' w={8} mr={40}>
            <CartIcon/>
            {totalQty > 0 && (
                <Badge
                    w='5'
                    h='5'
                    display='flex'
                    justifyContent='center'
                    alignItems='center'
                    position='absolute'
                    top='-3'
                    right='-3'
                    bg='orange.500'
                    color='white'
                    borderRadius='50%'
                >
                    {totalQty}
                </Badge>
            )}
        </Box>
    </Link>
}