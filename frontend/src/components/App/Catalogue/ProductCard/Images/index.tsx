import {ImagePagination, ImagePaginationWrapper} from "@/components/App/Catalogue/ProductCard/components";
import {Box} from "@chakra-ui/react";
import React, {useState} from "react";
import {SkuInterface} from "@/components/App/Catalogue/ProductCard/interfaces";
import {MEDIA_URL} from "@/local";
import {ProductImage} from "@/components/App/Catalogue/ProductCard/style";


interface CatalogueProductImagesProps {
  sku: SkuInterface
}


export const CatalogueProductImages = ({sku}: CatalogueProductImagesProps) => {
  const [imageIndex, setImageIndex] = useState<number>(0)
  const imagesQty: number = sku.images.length

  return <Box pos="relative" display="block" w="100%" h="auto" pt="66%">
    <ImagePaginationWrapper>
      {Array.from({length: imagesQty}, (_, key) =>
        <ImagePagination onHover={() =>  setImageIndex(key)} key={key}/>)}
    </ImagePaginationWrapper>
    <ProductImage unoptimized fill src={MEDIA_URL + sku.images[imageIndex]} alt={'img'}/>
  </Box>
}