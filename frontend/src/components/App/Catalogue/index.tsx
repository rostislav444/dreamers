import {Box, Grid} from "@chakra-ui/react";
import {ProductCard} from "@/components/App/Catalogue/ProductCard";


interface ProductsListInterface {
    products: any[]
}


export const ProductsList = ({products}: ProductsListInterface) => {
    return <Box mt={8}>
        <Grid templateColumns='repeat(auto-fill, minmax(340px, 1fr))' gap={4}>
            {
                products.map((product, key) =>
                    <ProductCard key={product.id} product={product}/>
                )
            }
        </Grid>
    </Box>
}


