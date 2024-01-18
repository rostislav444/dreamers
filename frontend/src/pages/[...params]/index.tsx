import Layout from "@/components/Shared/Layout";
import {ProductsList} from "src/components/App/Catalogue";
import type {GetStaticPaths, GetStaticProps,} from 'next'
import fetchApi from "@/utils/fetch";
import ErrorPage from 'next/error'

interface CatalogueProps {
    products: any
}


export default function Catalogue({products}: CatalogueProps) {
    const breadcrumbs = [
        {title: 'Главная', link: '/'},
        {title: 'Каталог'},
    ]

    if (!products) {
        return <ErrorPage statusCode={404}/>;
    }

    return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'Каталог'}>
        <ProductsList products={products}/>
    </Layout>

}


export const getStaticProps = (async (context) => {
    const api = fetchApi()
    const response = await api.get('catalogue/products/')

    if (response.ok) {
        return {
            props: {products: response.data},
            revalidate: 60 * 5,
        }
    }

    return {notFound: true}
}) satisfies GetStaticProps<{ products: any }>


export const getStaticPaths = (async () => {
    return {
        paths: [
            '/catalogue'
        ],
        fallback: 'blocking',
    }
}) satisfies GetStaticPaths