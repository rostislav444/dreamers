import {Box} from "@chakra-ui/react";
import React, {useState} from "react";
import {ProductCardProps} from "@/components/App/Catalogue/ProductCard/interfaces";
import {MEDIA_URL} from "@/local";
import {ProductImage} from "@/components/App/Catalogue/ProductCard/style";


interface ImageInterface {
    thumbnails: {
        s: string;
        m: string;
    };
    image: string;
}

interface Props {
    images: ImageInterface[]
}

// https://eu-north-1.console.aws.amazon.com/s3/buckets/dreamers/komod-1_w1200_h1750_d400/product/productpartscenematerialimage/25553/image-jseprw_m.png
// https://dreamers.s3.eu-north-1.amazonaws.com/komod-2_w1200_h1350_d400/product/productpartscenematerialimage/26783/image-aspzid.png


export const CatalogueProductImages = ({images}: Props) => {
    return <Box pos="relative" display="block" w="100%" h="auto" pt="66%">
        {images.reverse().map((image: ImageInterface, key: number) => <ProductImage key={key} src={MEDIA_URL + image.thumbnails?.m} alt={'img'}/>)}
    </Box>
}