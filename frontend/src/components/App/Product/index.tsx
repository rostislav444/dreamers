import {ProductProps} from "@/interfaces/Product";
import {useState} from "react";
import {ProductGallery} from "@/components/App/Product/Galery";
import {Box, Grid, GridItem, useMediaQuery} from "@chakra-ui/react";
import {ProductInfo} from "@/components/App/Product/Info";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {parseMaterialsWithDefaults} from "@/utils/Product/Materials";


export const ProductComponent = ({product, materials}: ProductProps) => {
    const [mobile] = useMediaQuery('(max-width: 960px)');

    const parsedMaterials = parseMaterialsWithDefaults(materials, product.material_parts);
    const [selectedMaterials, setSelectedMaterials] = useState<SelectedMaterialsInterface>(parsedMaterials)

    return <Box>
        <Grid mb='2' gridTemplateColumns={mobile ? '1fr' : '3fr 1fr'}>
            <GridItem>
                <ProductGallery mobile={mobile} product={product} selectedMaterials={selectedMaterials}/>
            </GridItem>
            <GridItem>
                <ProductInfo mobile={mobile} product={product} selectedMaterials={selectedMaterials}
                             setSelectedMaterials={setSelectedMaterials}/>
            </GridItem>
        </Grid>
    </Box>

}