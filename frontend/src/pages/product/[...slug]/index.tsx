import Layout from "@/components/Shared/Layout";
import fetchApi from "@/utils/fetch";
import {GetStaticPaths, GetStaticProps} from "next";
import {ProductProps} from "@/interfaces/Product";
import {CategoryState} from "@/interfaces/Categories";
import {ProductComponent} from "@/components/App/Product";


const processBreadCrumbs = (categories: CategoryState[], name: string, code: string) => {
    // Создаем хлебные крошки с накопительными ссылками
    const breadcrumbs = categories.map((category, index) => ({
        title: category.name,
        link: `/catalogue/${categories.slice(0, index + 1).map(cat => cat.slug).join('/')}`
    }));

    // Добавляем текущий продукт
    breadcrumbs.push({
        title: name,
        link: `/product/${code}`
    });

    return breadcrumbs;
};

const Product = ({product, materials}: ProductProps) => {
    return <Layout breadcrumbs={processBreadCrumbs(product.categories, product.name, product.code)}
                   description={'description'} title={product.name}>
        <ProductComponent product={product} materials={materials}/>
    </Layout>
}


export const getStaticProps = (async ({params}) => {
    const slug = params?.slug;

    if (!slug) {
        return {notFound: true};
    }

    const api = fetchApi();
    const response = await api.get(`product/product/${slug[0]}`);

    if (response.ok) {
        return {
            props: {product: response.data, materials: slug[1] || null},
            revalidate: 60 * 5,
        };
    }
    return {notFound: true};
}) as GetStaticProps<{ products: any; }>;


export const getStaticPaths = (async () => {
    const api = fetchApi()
    const response = await api.get('product/products_list')
    const paths = response.data.products.map((product: string) => `/product/${product}`)

    return {
        paths,
        fallback: 'blocking',
    }
}) satisfies GetStaticPaths


export default Product;