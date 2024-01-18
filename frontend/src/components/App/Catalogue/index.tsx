import {Box, Grid, GridItem} from "@chakra-ui/react";
import {ProductCard} from "@/components/App/Catalogue/ProductCard";


interface ProductsListInterface {
  products: any[]
}


export const ProductsList = ({products}: ProductsListInterface) => {
  return <Box mt={8}>
    <Grid templateColumns='repeat(auto-fill, minmax(340px, 1fr))' gap={0}>
      {
        products.map((product, key) =>
          <GridItem position={'relative'} key={key} >
            <ProductCard product={product}/>
          </GridItem>
        )
      }
    </Grid>
  </Box>
}


