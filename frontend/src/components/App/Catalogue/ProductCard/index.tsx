import React, {useState} from "react";
import {Box} from "@chakra-ui/react";
import {ProductCardMaterial} from "@/components/App/Catalogue/ProductCard/Materials";
import {ProductCardProps} from "@/components/App/Catalogue/ProductCard/interfaces";
import {CatalogueProductImages} from "@/components/App/Catalogue/ProductCard/Images";
import Link from "next/link";


export const ProductCard: React.FC<ProductCardProps> = ({product}) => {
    const [selectedSku, setSelectedSku] = useState<number | null>(null)
    const sku = product.sku[selectedSku || 0]

    return (
        <Box
            borderWidth="3px"
            borderColor={"brown.500"}
            overflow="hidden"
        >
            <Link href={`/product/${product.code}`}>
                <CatalogueProductImages sku={sku}/>
            </Link>
            <Box p="4">
                <Link href={`/product/${product.code}`}>
                    <Box fontWeight="semibold" as="h4" lineHeight="tight" noOfLines={1} pb={2}>
                        {product.name}
                    </Box>
                </Link>
                <ProductCardMaterial
                    product={product}
                    setSelectedSku={setSelectedSku}
                />
                <Box>
                    <Box as="span" fontSize="l">
                        {product.price} {"грн."}
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};
