import {Box} from "@chakra-ui/react";
import React, {useState} from "react";
import {ProductCardProps} from "@/components/App/Catalogue/ProductCard/interfaces";
import {MEDIA_URL} from "@/local";
import {ProductImage} from "@/components/App/Catalogue/ProductCard/style";


interface CatalogueProductImagesProps {
    product: ProductCardProps
}


export const CatalogueProductImages = ({product}: CatalogueProductImagesProps) => {
    const [imageIndex, setImageIndex] = useState<number>(0)
    const imagesQty: number = 1

    console.log(product)

    return <Box pos="relative" display="block" w="100%" h="auto" pt="66%">
        {/*<ImagePaginationWrapper>*/}
        {/*    {Array.from({length: imagesQty}, (_, key) =>*/}
        {/*        <ImagePagination onHover={() => setImageIndex(key)} key={key}/>)}*/}
        {/*</ImagePaginationWrapper>*/}
        {/*<ProductImage unoptimized fill src={MEDIA_URL + sku.images[imageIndex]} alt={'img'}/>*/}

        {product.part_images.map((image, key) => {
            return <ProductImage key={key} src={MEDIA_URL + image} alt={'img'}/>
        })}


    </Box>
}