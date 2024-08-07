import {ProductProps} from "@/interfaces/Product";
import {useState} from "react";
import {ProductGallery} from "@/components/App/Product/Galery";
import {Flex, Grid, GridItem, useMediaQuery} from "@chakra-ui/react";
import {ProductInfo} from "@/components/App/Product/Info";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {setFirstMaterials, setInitialMaterials} from "@/utils/Product/Materials";


export const ProductComponent = ({product, materials}: ProductProps) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');
    const parseMaterials = (materials: string) => {
        return Object.fromEntries(
            materials.split('_').slice(1).map(pair => pair.split('-').map(Number))
        );
    };

    const parsedMaterials = materials ? parseMaterials(materials) : setFirstMaterials(product.material_parts);
    const [selectedMaterials, setSelectedMaterials] = useState<SelectedMaterialsInterface>(parsedMaterials)


    return <Grid mb='2' gridTemplateColumns={mobile ? '1fr' : '3fr 1fr'}>
        <GridItem>
            <ProductGallery mobile={mobile} product={product} selectedMaterials={selectedMaterials}/>
        </GridItem>
        <GridItem>
            <ProductInfo mobile={mobile} product={product} selectedMaterials={selectedMaterials}
                         setSelectedMaterials={setSelectedMaterials}/>
        </GridItem>
    </Grid>
}