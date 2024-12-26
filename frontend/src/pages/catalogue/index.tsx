import Layout from "@/components/Shared/Layout";
import {ProductsList} from "src/components/App/Catalogue";
import type {GetStaticProps,} from 'next'
import fetchApi from "@/utils/fetch";

import {CategoriesList} from "@/components/App/Catalogue/CategoriesList";

interface CatalogueProps {
    products: any,
    categories: any
}

interface CategoryInterface {
    id: number;
    name: string;
    slug: string;
    children: CategoryInterface[] | null;
}



export default function Catalogue({products, categories}: CatalogueProps) {
    const breadcrumbs = [
        {title: 'Каталог'},
    ]


    if (!products) {
        return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
            <h1>Нет товаров</h1>
        </Layout>
    }

    return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
        <CategoriesList categories={categories} />
        <ProductsList products={products}/>
    </Layout>

}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const productsResp = await api.get('catalogue/products/', {}, true);
    const categoriesResp = await api.get('category', {}, true);

    if (productsResp.ok) {
        return {
            props: {
                products: productsResp.data.results,
                categories: categoriesResp.ok ? categoriesResp.data.results : []
            },
            revalidate: 60 * 5,
        }
    }

    return {notFound: true}
}) satisfies GetStaticProps<{ products: any }>



