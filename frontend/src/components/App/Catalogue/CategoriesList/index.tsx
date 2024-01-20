import {RecursiveCategoryInterface} from "@/interfaces/Categories";
import {Grid, GridItem} from "@chakra-ui/react";
import Link from 'next/link'


interface CategoriesListProps {
    categories: RecursiveCategoryInterface[]
}

export const CategoriesList = ({categories}: CategoriesListProps) => {
    return <Grid gridTemplateColumns='repeat(auto-fill, minmax(240px, 1fr))' gap='2' mb='10'>
        {categories.map(category =>
            <Link key={category.id} href={'/catalogue/' + category.slug}>
                <GridItem
                    p={4}
                    border='3px solid'
                    bg='brown.100'
                    textAlign='center'
                    _hover={{
                        bg: 'brown.500',
                        color: 'brown.50'
                    }}
                >{category.name}</GridItem>
            </Link>
        )}
    </Grid>

}