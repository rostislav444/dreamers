import {Box, Button, Flex, Grid, Image, Text} from "@chakra-ui/react";
import Link from "next/link";
import InspirationBlock from "@/components/App/Home/InspirationBlock";
import {CategoryState} from "@/interfaces/Categories";
import {ProductInterface} from "@/interfaces/Product";
import {ProductCard} from "@/components/App/Catalogue/ProductCard";
import {CatalogueProductImages} from "@/components/App/Catalogue/ProductCard/Images";
import {MEDIA_URL} from "@/local";


interface Props {
    categories: CategoryState[]
    products: ProductInterface[]
}

const ResponsiveHero = ({categories, products}: Props) => {
    const categoriesResponsive = categories.map((category, index) => {
        return {
            ...category,
            colSpan: {base: 12, sm: 12, md: index === 0 ? 8 : 4},
            rowSpan: {base: 1, sm: 1, md: 2},
            height: {base: "300px", sm: "400px", md: "400px"}
        }
    })


    return (
        <Box width="100%" bg="brown.50">
            {/* Hero Content Container */}
            <Box width="100%">
                {/* Hero Text */}
                <Box
                    maxW={{base: "100%", lg: "80%", xl: "60%"}}
                    mb={{base: 6, md: 10}}
                >
                    <Text
                        as="h1"
                        fontSize={{base: "3xl", sm: "4xl", md: "5xl", lg: "6xl"}}
                        fontWeight="bold"
                        color='brown.500'
                        lineHeight="1.2"
                        mb={4}
                    >
                        Знайдіть свої<br/>ідеальні меблі
                    </Text>
                    <Text
                        fontSize={{base: "md", sm: "lg", md: "xl"}}
                        color='brown.500'
                        maxW={{base: "100%", md: "80%", lg: "70%"}}
                        mb={6}
                    >
                        Ми допоможемо вам створити простір вашої мрії.
                        Оберіть свій стиль разом з нами.
                    </Text>
                    <Flex
                        gap={4}
                        flexWrap="wrap"
                    >
                        <Link href='/catalogue'>
                            <Button
                                bg='brown.500'
                                color="white"
                                _hover={{bg: "brown.800"}}
                                size={{base: "md", md: "lg"}}
                                px={{base: 6, md: 8}}
                                py={{base: 4, md: 6}}
                            >
                                Каталог
                            </Button>
                        </Link>
                        <Button
                            variant="outline"
                            borderColor='brown.500'
                            borderWidth={2}
                            color='brown.500'
                            _hover={{bg: "brown.100"}}
                            size={{base: "md", md: "lg"}}
                            px={{base: 6, md: 8}}
                            py={{base: 3, md: 5}}
                        >
                            Консультація
                        </Button>
                    </Flex>
                </Box>

                {/* Category Grid */}
                <Grid
                    templateColumns="repeat(12, 1fr)"
                    gap={{base: 4, md: 6, lg: 8}}
                    templateRows="auto"
                    width="100%"
                >
                    {categoriesResponsive.map((category) => (
                        <Box
                            key={category.name}
                            gridColumn={`span ${category.colSpan.base}`}
                            // gridRow={`span ${category.rowSpan.base as number}`}
                            sx={{
                                '@media screen and (min-width: 30em)': {
                                    gridColumn: `span ${category.colSpan.sm}`
                                },
                                '@media screen and (min-width: 48em)': {
                                    gridColumn: `span ${category.colSpan.md}`
                                }
                            }}
                            as={Link}
                            href={`/catalogue/${category.slug}`}
                            position="relative"
                            height={category.height}
                            overflow="hidden"
                            transition="all 0.3s"
                            _hover={{
                                transform: "translateY(-4px)",
                                shadow: "xl"
                            }}
                        >
                            {category.image.map((image, key) =>
                                <Image
                                    src={MEDIA_URL + image}
                                    pos='absolute'
                                    top='0'
                                    left='0'
                                    width='100%'
                                    height='100%'
                                    objectFit='contain'
                                    key={key} alt='image'/>
                            )}
                            <Box
                                position="absolute"
                                bottom={0}
                                left={0}
                                right={0}
                                p={{base: 4, md: 6}}
                                background="linear-gradient(to top, rgba(255,255,255,1), rgba(255,255,255,0))"
                            >
                                <Text
                                    fontSize={{base: "xl", sm: "2xl", md: "3xl"}}
                                    fontWeight="bold"
                                    color="brown.500"
                                >
                                    {category.name}
                                </Text>
                            </Box>
                        </Box>
                    ))}
                </Grid>
                {/* New Arrivals */}
                <Box mt='16' mb={16}>
                    <Flex justify="space-between" align="center" mb={6}>
                        <Text
                            fontSize={{base: "2xl", md: "3xl"}}
                            fontWeight="bold"
                            color="brown.900"
                        >
                            Нові надходження
                        </Text>
                        <Link href='/catalogue'>
                            <Button
                                variant="link"
                                color="brown.800"
                                _hover={{color: "brown.600"}}
                            >
                                Дивитись все
                            </Button>
                        </Link>
                    </Flex>

                    <Grid templateColumns='repeat(auto-fill, minmax(280px, 1fr))' gap={4}>
                        {products.map((item) => <ProductCard key={item.id} product={item}/>)}
                    </Grid>

                    {/* Цитата */}
                    <InspirationBlock/>
                </Box>
            </Box>
        </Box>
    );
};

export default ResponsiveHero;