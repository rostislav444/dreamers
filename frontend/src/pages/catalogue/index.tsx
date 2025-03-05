import Layout from "@/components/Shared/Layout";
import {ProductsList} from "@/components/App/Catalogue";
import {GetStaticProps} from 'next';
import {useRouter} from 'next/router';
import fetchApi from "@/utils/fetch";
import {CategoriesList} from "@/components/App/Catalogue/CategoriesList";
import {useState, useEffect} from "react";

interface CatalogueProps {
    initialProducts: any[];
    totalCount: number;
    initialNextPage: string | null;
    initialPreviousPage: string | null;
    categories: any[];
}

export default function Catalogue({
    initialProducts, 
    totalCount, 
    initialNextPage,
    initialPreviousPage,
    categories
}: CatalogueProps) {
    const router = useRouter();
    const [products, setProducts] = useState(initialProducts);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [hasNext, setHasNext] = useState(!!initialNextPage);
    const [hasPrevious, setHasPrevious] = useState(!!initialPreviousPage);
    
    const PAGE_SIZE = 24;
    
    const breadcrumbs = [
        {title: 'Каталог'},
    ];
    
    useEffect(() => {
        // Get page from URL or default to 1
        const pageFromQuery = Number(router.query.page) || 1;
        if (pageFromQuery !== currentPage) {
            setCurrentPage(pageFromQuery);
        }
    }, [router.query.page, currentPage]);
    
    useEffect(() => {
        // Skip the first render since we already have initial products
        if (currentPage === 1 && products === initialProducts) return;
        
        const fetchProducts = async () => {
            setLoading(true);
            const api = fetchApi();
            const response = await api.get('catalogue/products/', {page: currentPage, page_size: PAGE_SIZE}, true);
            
            if (response.ok) {
                setProducts(response.data.results);
                setHasNext(!!response.data.next);
                setHasPrevious(!!response.data.previous);
            }
            setLoading(false);
        };
        
        fetchProducts();
    }, [currentPage, initialProducts, products]);
    
    const handlePageChange = (page: number) => {
        // Update URL with new page
        router.push({
            pathname: router.pathname,
            query: {...router.query, page}
        }, undefined, {shallow: true});
        
        // Page state is updated by the useEffect that watches router.query
    };
    
    return (
        <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
            <CategoriesList categories={categories} />
            <ProductsList 
                products={products} 
                totalCount={totalCount} 
                currentPage={currentPage}
                onPageChange={handlePageChange}
                hasNext={hasNext}
                hasPrevious={hasPrevious}
            />
        </Layout>
    );
}

export const getStaticProps = (async (context) => {
    const api = fetchApi();
    const productsResp = await api.get('catalogue/products/', {page: 1, page_size: 24}, true);
    const categoriesResp = await api.get('category', {}, true);

    if (productsResp.ok) {
        return {
            props: {
                initialProducts: productsResp.data.results,
                totalCount: productsResp.data.count,
                initialNextPage: productsResp.data.next,
                initialPreviousPage: productsResp.data.previous,
                categories: categoriesResp.ok ? categoriesResp.data.results : []
            },
            revalidate: 60 * 5,
        };
    }

    return {notFound: true};
}) satisfies GetStaticProps;

