import Layout from "@/components/Shared/Layout";
import {ProductsList} from "src/components/App/Catalogue";
import type {GetStaticPaths, GetStaticProps,} from 'next'
import fetchApi from "@/utils/fetch";
import ErrorPage from 'next/error'
import {CategoriesList} from "@/components/App/Catalogue/CategoriesList";

interface CatalogueProps {
    products: any,
    categories: any
}


export default function Catalogue({products, categories}: CatalogueProps) {
    const breadcrumbs = [
        {title: 'Каталог'},
    ]

    if (!products) {
        return <ErrorPage statusCode={404}/>;
    }

    return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
        <CategoriesList categories={categories} />
        <ProductsList products={products}/>
    </Layout>

}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const productsResp = await api.get('catalogue/products/')
    const categoriesResp = await api.get('category');

    if (productsResp.ok) {
        return {
            props: {
                products: productsResp.data,
                categories: categoriesResp.ok ? categoriesResp.data : []
            },
            revalidate: 60 * 5,
        }
    }

    return {notFound: true}
}) satisfies GetStaticProps<{ products: any }>

interface CategoryInterface {
    id: number;
    name: string;
    slug: string;
    children: CategoryInterface[] | null;
}


