import {Box} from "@chakra-ui/react";
import React, {useState} from "react";
import {ProductCardProps} from "@/components/App/Catalogue/ProductCard/interfaces";
import {MEDIA_URL} from "@/local";
import {ProductImage} from "@/components/App/Catalogue/ProductCard/style";


interface Props {
    images: string[]
}


export const CatalogueProductImages = ({images}: Props) => {
    return <Box pos="relative" display="block" w="100%" h="auto" pt="66%">
        {images.map((image: string, key: number) => <ProductImage key={key} src={MEDIA_URL + image} alt={'img'}/>)}
    </Box>
}