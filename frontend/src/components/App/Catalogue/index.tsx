import {Box, Grid, Text} from "@chakra-ui/react";
import {ProductCard} from "@/components/App/Catalogue/ProductCard";
import {ProductInterface} from "@/interfaces/Product";
import {PaginatedData} from "@/utils/fetch";
import { Pagination } from "@/components/Shared/Pagination";


interface ProductsListInterface {
    products: ProductInterface[];
    totalCount?: number;
    currentPage?: number;
    onPageChange?: (page: number) => void;
    hasNext?: boolean;
    hasPrevious?: boolean;
}


export const ProductsList = ({
    products, 
    totalCount = 0, 
    currentPage = 1, 
    onPageChange,
    hasNext = false,
    hasPrevious = false
}: ProductsListInterface) => {
    const PAGE_SIZE = 24;
    const totalPages = Math.ceil(totalCount / PAGE_SIZE);
    
    if (products.length === 0) {
        return (
            <Box mt={8} textAlign="center">
                <Text fontSize="xl">Нет товаров</Text>
            </Box>
        );
    }
    
    return (
        <Box mt={8}>
            <Grid templateColumns='repeat(auto-fill, minmax(340px, 1fr))' gap={4}>
                {
                    products.map((product) =>
                        <ProductCard key={product.id} product={product}/>
                    )
                }
            </Grid>
            
            {onPageChange && totalCount > PAGE_SIZE && (
                <Pagination 
                    currentPage={currentPage} 
                    totalPages={totalPages} 
                    onPageChange={onPageChange}
                    hasNext={hasNext}
                    hasPrevious={hasPrevious}
                />
            )}
        </Box>
    );
}


