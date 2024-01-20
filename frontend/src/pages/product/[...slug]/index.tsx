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


interface ProductProps {
    product: ProductInterface,
    skuId?: string
}


const Product = ({product, skuId}: ProductProps) => {
    const {addItem} = useCart()
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const router = useRouter();

    const skuInitial = product.sku.findIndex(item => String(item.id) === skuId)
    const [selectedSku, setSelectedSku] = useState<number>(skuInitial > 0 ? skuInitial : 0)

    if (!product.sku) {
        return <ErrorPage statusCode={404}/>;
    }

    const currentSku = product.sku[selectedSku]

    const materialsSelected = product.parts.map(part => {
        const materialGroup = part.material_groups.find(materialGroup =>
            materialGroup.materials.some(mat => mat.id === currentSku.materials[part.id])
        );

        const material = materialGroup?.materials.find(mat => mat.id === currentSku.materials[part.id]);

        return {
            name: part.name,
            material: material
        };
    });


    const images = currentSku.images

    const selectSkuByMaterials = (material: any) => {
        const newSkuIndex = getBestFitSku({...currentSku.materials, ...material}, product.sku)
        setSelectedSku(newSkuIndex)
    }

    const handleAddCartItem = () => {
        const payload = {
            product: product.id,
            sku: currentSku.id,
            name: product.name,
            code: product.code,
            price: product.price,
            qty: 1,
            image: currentSku.images[0].image,
            material: {
                color: ''
            }
        }
        addItem(payload)
        router.push('/order')
    }

    return <Layout breadcrumbs={processBreadCrumbs(product.categories, product.name, product.code)}
                   description={'description'} title={product.name}>
        <Flex
            mb='2'
            flexDir={mobile ? 'column' : 'row'}
        >
            <ProductGallery images={images}/>
            <Box w={mobile ? '100%' : '45%'} pl={mobile ? 0 : 4} mt={mobile ? 8 : 0}>
                <Heading mb={mobile ? 4 : 8}>{product.name}</Heading>
                <InfoHeading mobile={mobile}>Колір</InfoHeading>
                <ProductMaterials
                    parts={product.parts}
                    materials={currentSku.materials}
                    selectSkuByMaterials={selectSkuByMaterials}
                />
                <ProductCharacteristics product={product} materialsSelected={materialsSelected}/>
                <InfoHeading mobile={mobile}>Опис</InfoHeading>
                <Text maxH='48' overflowY="hidden" fontSize={14} mt={4}>{product.description}</Text>
                <Text color={'brown.500'} fontSize={24} mt={8}>{product.price} грн.</Text>
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
    const response = await api.get(`product/product/${slug[0]}`);

    if (response.ok) {
        return {
            props: {product: response.data, skuId: slug[1]},
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