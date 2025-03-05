import Layout from "@/components/Shared/Layout";
import {ProductsList} from "@/components/App/Catalogue";
import {GetStaticProps} from 'next';
import {useRouter} from 'next/router';
import fetchApi from "@/utils/fetch";
import ErrorPage from 'next/error';
import {RecursiveCategoryInterface} from "@/interfaces/Categories";
import {useState, useEffect} from "react";

interface CatalogueProps {
    initialProducts: any[];
    totalCount: number;
    categories: any[];
}

interface CatalogueProps {
    initialProducts: any[];
    totalCount: number;
    initialNextPage: string | null;
    initialPreviousPage: string | null;
    categories: any[];
}

export default function CatalogueCategory({
    initialProducts, 
    totalCount, 
    initialNextPage,
    initialPreviousPage,
    categories = []
}: CatalogueProps) {
    const router = useRouter();
    const [products, setProducts] = useState(initialProducts);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [hasNext, setHasNext] = useState(!!initialNextPage);
    const [hasPrevious, setHasPrevious] = useState(!!initialPreviousPage);
    
    const PAGE_SIZE = 24;
    
    const breadcrumbs = [
        {title: 'Каталог', link: '/catalogue'},
        ...categories.map(category => ({title: category.name}))
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
        
        if (!router.isReady) return;
        
        const fetchProducts = async () => {
            setLoading(true);
            const api = fetchApi();
            const categoryParams = router.query.categories as string[];
            
            if (!categoryParams) {
                setLoading(false);
                return;
            }
            
            const response = await api.get(
                'catalogue/products/', 
                {
                    categories: categoryParams.join(','),
                    page: currentPage, 
                    page_size: PAGE_SIZE
                }, 
                true
            );
            
            if (response.ok) {
                setProducts(response.data.results);
                setHasNext(!!response.data.next);
                setHasPrevious(!!response.data.previous);
            }
            setLoading(false);
        };
        
        fetchProducts();
    }, [currentPage, router.isReady, router.query.categories, initialProducts, products]);
    
    const handlePageChange = (page: number) => {
        // Update URL with new page
        router.push({
            pathname: router.pathname,
            query: {...router.query, page}
        }, undefined, {shallow: true});
        
        // Page state is updated by the useEffect that watches router.query
    };
    
    if (!initialProducts) {
        return <ErrorPage statusCode={404}/>;
    }
    
    return (
        <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
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

export const getStaticProps: GetStaticProps = async ({params}) => {
    if (!params || !('categories' in params)) {
        return {notFound: true};
    }
    
    const api = fetchApi();
    const {categories} = params as { categories: string[] };
    
    const categoryResp = await api.get('category/?categories=' + categories.join(','), {}, true);
    const productsResp = await api.get(
        'catalogue/products/', 
        {
            categories: categories.join(','),
            page: 1,
            page_size: 24
        }, 
        true
    );
    
    if (productsResp.ok) {
        return {
            props: {
                initialProducts: productsResp.data.results,
                totalCount: productsResp.data.count,
                initialNextPage: productsResp.data.next,
                initialPreviousPage: productsResp.data.previous,
                categories: categoryResp.ok ? categoryResp.data.results : []
            },
            revalidate: 60 * 5,
        };
    }
    
    return {notFound: true};
};


export const getStaticPaths = async () => {
    const getFlatCategories = (categories: RecursiveCategoryInterface[], parentPath = '/catalogue'): string[] => {
        return categories.reduce<string[]>((flatCategories, category) => {
            const path = `${parentPath}/${category.slug}`;
            flatCategories.push(path);

            if (category.children && category.children.length > 0) {
                flatCategories.push(...getFlatCategories(category.children, path));
            }

            return flatCategories
        }, []);
    };

    try {
        const api = fetchApi();
        const response = await api.get('category', {}, true);


        if (response.ok) {
            const paths = getFlatCategories(response.data.results);

            return {
                paths,
                fallback: 'blocking',
            };
        }
    } catch (error) {
        console.error('Error fetching category data:', error);
    }

    // Return a default fallback
    return {
        paths: [],
        fallback: 'blocking',
    };
};