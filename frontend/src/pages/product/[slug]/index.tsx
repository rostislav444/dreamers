import {Box, Button, Flex, Heading, Text, useMediaQuery} from "@chakra-ui/react";
import Layout from "@/components/Shared/Layout";
import fetchApi from "@/utils/fetch";
import {GetStaticPaths, GetStaticProps} from "next";
import {ProductInterface} from "@/interfaces/Product";
import {useState} from "react";
import {ProductGallery} from "@/components/App/Product/Galery";
import {ProductMaterials} from "@/components/App/Product/Materials";
import {getBestFitSku} from "@/utils/Product/sku";
import {ProductCharacteristics} from "@/components/App/Product/Info/Characteristic";
import {InfoHeading} from "@/components/Shared/Typogrphy";
import {useCart} from "@/context/Cart";
import {useRouter} from "next/router";
import ErrorPage from "next/error";
import {CategoryState} from "@/interfaces/Categories";


const processBreadCrumbs = (categories: CategoryState[], name: string, code: string) => ([
    ...categories.map(category => ({title: category.name, link: '/catalogue'})),
    {title: name, link: `/product/${code}`},
])


const Product = (product: ProductInterface) => {
    const {addItem} = useCart()
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const router = useRouter();
    const {id, name, code, price, sku, parts, categories, width, height, depth} = product
    const [selectedSku, setSelectedSku] = useState<number>(0)
    const [isLessThen960] = useMediaQuery('(max-width: 1150px)')

    if (!product.sku) {
        return <ErrorPage statusCode={404}/>;
    }

    const currentSku = sku[selectedSku]
    const images = currentSku.images

    const selectSkuByMaterials = (material: any) => {
        const newSkuIndex = getBestFitSku({...currentSku.materials, ...material}, sku)
        setSelectedSku(newSkuIndex)
    }

    const handleAddCartItem = () => {
        const payload = {
            product: id,
            sku: currentSku.id,
            name,
            code,
            price,
            qty: 1,
            image: currentSku.images[0].image,
            material: {
                color: ''
            }
        }
        addItem(payload)
        router.push('/cart')
    }


    return <Layout breadcrumbs={processBreadCrumbs(categories, name, code)} description={'description'} title={name}>
        <Flex
            mb='2'
            flexDir={mobile ? 'column' : 'row'}
        >
            <ProductGallery images={images}/>
            <Box w={mobile ? '100%' : '45%'} pl={mobile ? 0 : 4} mt={mobile ? 8 : 0}>
                <Heading mb={mobile ? 4 : 8}>{name}</Heading>
                <InfoHeading mobile={mobile}>Колір</InfoHeading>
                <ProductMaterials
                    parts={parts}
                    materials={currentSku.materials}
                    selectSkuByMaterials={selectSkuByMaterials}
                />
                <ProductCharacteristics product={product}/>
                <InfoHeading mobile={mobile}>Опис</InfoHeading>
                <Text maxH='48' overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
                <Text color={'brown.500'} fontSize={24} mt={8}>{price} грн.</Text>
                <Button w={'100%'} mt={8} p={6} onClick={handleAddCartItem}>Придбати</Button>
            </Box>
        </Flex>
    </Layout>
}


export const getStaticProps = (async ({params}) => {
    const slug = params?.slug;

    if (!slug) {
        return {notFound: true};
    }

    const api = fetchApi();
    const response = await api.get(`product/product/${slug}`);

    if (response.ok) {
        return {
            props: response.data,
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