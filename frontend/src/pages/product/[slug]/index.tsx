import {Box, Button, Heading, Text, useMediaQuery} from "@chakra-ui/react";
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


const Product = (product: ProductInterface) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const router = useRouter();
    const {id, name, code, price, sku, parts, categories, width, height, depth} = product
    const [selectedSku, setSelectedSku] = useState<number>(0)
    const currentSku = sku[selectedSku]
    const images = currentSku.images

    const [isLessThen960] = useMediaQuery('(max-width: 1150px)')
    const {addItem} = useCart()

    const breadcrumbs = [
        ...categories.map(category => ({title: category.name, link: '/catalogue'})),
        {title: name, link: `/product/${code}`},
    ]

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


    return <Layout breadcrumbs={breadcrumbs} description={'description'} title={'title'}>
        <Box
            mb='2'
            display='grid'
            gridTemplateColumns={isLessThen960 ? '1fr' : '55fr 45fr'}
            gap={2}
        >
            <ProductGallery images={images}/>
            <Box pl={mobile ? 0: 4}>
                <Heading mb={mobile ? 4 : 8}>{name}</Heading>
                <ProductCharacteristics product={product}/>
                <InfoHeading mobile={mobile}>Колір</InfoHeading>
                <ProductMaterials
                    parts={parts}
                    materials={currentSku.materials}
                    selectSkuByMaterials={selectSkuByMaterials}
                />
                <Text color={'brown.500'} fontSize={24} mt={8}>{price} грн.</Text>
                <Button w={'100%'} mt={8} p={6} onClick={handleAddCartItem}>Придбати</Button>
                <InfoHeading mobile={mobile}>Опис</InfoHeading>
                <Text maxH='48'  overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
            </Box>
        </Box>
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
        return {props: response.data};
    }
    return {notFound: true};
}) as GetStaticProps<{
    products: any;
}>;


export const getStaticPaths = (async () => {
    const api = fetchApi()
    const response = await api.get('product/products_list')
    const paths = response.data.products.map((product: string) => `/product/${product}`)

    return {
        paths,
        fallback: true,
    }
}) satisfies GetStaticPaths


export default Product;