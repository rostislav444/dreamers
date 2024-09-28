import Layout from "@/components/Shared/Layout";
import {ProductsList} from "src/components/App/Catalogue";
import type {GetStaticProps,} from 'next'
import fetchApi from "@/utils/fetch";
import ErrorPage from 'next/error'
import {RecursiveCategoryInterface} from "@/interfaces/Categories";

interface CatalogueProps {
    products: any,
    categories: any[]
}


export default function CatalogueCategory({products, categories = []}: CatalogueProps) {
    const breadcrumbs = [
        {title: 'Каталог', link: '/catalogue'},
        ...categories.map(category => ({title: category.name}))
    ]

    if (!products) {
        return <ErrorPage statusCode={404}/>;
    }

    return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
        <ProductsList products={products}/>
    </Layout>

}


export const getStaticProps: GetStaticProps = async ({params}) => {
    if (!params || !('categories' in params)) {
        return {notFound: true};
    }

    const api = fetchApi();
    const {categories} = params as { categories: string[] };

    const categoryResp = await api.get('category/?categories=' + categories.join(','));
    const productsResp = await api.get('catalogue/products/?categories=' + categories.join(','));

    if (productsResp.ok) {
        return {
            props: {
                products: productsResp.data,
                categories: categoryResp.ok ? categoryResp.data : []
            },
            revalidate: 60 * 5,
        };
    }

    return {notFound: true};
};


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

export const getStaticPaths = async () => {
    try {
        const api = fetchApi();
        const response = await api.get('category');

        if (response.ok) {
            const paths = getFlatCategories(response.data);

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