import Layout from '@/components/Shared/Layout'
import fetchApi from "@/utils/fetch";
import type {GetStaticProps} from "next";
import ResponsiveHero from "@/components/App/Home/ResponsiveHeroSection";
import {ProductInterface} from "@/interfaces/Product";
import {CategoryState} from "@/interfaces/Categories";


interface Props {
    categories: CategoryState[]
    products: ProductInterface[]
}


export default function Home({categories, products}: Props) {
    return (
        <Layout breadcrumbs={[]} description='description' title='Меблі, що надихаюь'>
            <ResponsiveHero categories={categories} products={products} />
        </Layout>
    )
}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const categoriesResp = await api.get('category', {}, true);
    const productsResp = await api.get('catalogue/products/', {limit: 4}, true);

    return {
        props: {
            categories: categoriesResp.ok ? categoriesResp.data.results : [],
            products: productsResp.ok ? productsResp.data.results : []
        },
        revalidate: 60 * 5,
    }

}) satisfies GetStaticProps<{ categories: any }>
