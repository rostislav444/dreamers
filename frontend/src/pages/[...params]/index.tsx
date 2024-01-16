import Layout from "@/components/Shared/Layout";
import {ProductsList} from "src/components/App/Catalogue";
import type {GetStaticPaths, GetStaticProps,} from 'next'
import fetchApi from "@/utils/fetch";


interface CatalogueProps {
    products: any
}


export default function Catalogue({products}: CatalogueProps) {
    const breadcrumbs = [
        {title: 'Главная', link: '/'},
        {title: 'Каталог'},
    ]

    return (
        <Layout breadcrumbs={breadcrumbs} description={'description'} title={'title'}>
            <ProductsList products={products}/>
        </Layout>
    )
}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const response = await api.get('catalogue/products/')
    if (response.ok) {
        return {props: {products: response.data}}
    }
    return {notFound: true}
}) satisfies GetStaticProps<{
    products: any
}>


export const getStaticPaths = (async () => {
    return {
        paths: [
            '/catalogue'
        ],
        fallback: true,
    }
}) satisfies GetStaticPaths