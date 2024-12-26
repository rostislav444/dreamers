import {Box, Grid} from "@chakra-ui/react";
import {ProductCard} from "@/components/App/Catalogue/ProductCard";
import {ProductInterface} from "@/interfaces/Product";
import {PaginatedData} from "@/utils/fetch";


interface ProductsListInterface {
    products: PaginatedData<ProductInterface>
}


export const ProductsList = ({products}: ProductsListInterface) => {
    const {results} = products

    return <Box mt={8}>
        <Grid templateColumns='repeat(auto-fill, minmax(340px, 1fr))' gap={4}>
            {
                results.map((product, key) =>
                    <ProductCard key={product.id} product={product}/>
                )
            }
        </Grid>
    </Box>
}


