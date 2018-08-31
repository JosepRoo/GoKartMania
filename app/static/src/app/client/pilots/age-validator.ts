import { AbstractControl, FormArray, FormGroup } from '@angular/forms';
export class AgeValidator {

    static ValidateAge(AC: AbstractControl) {
        let type = AC.get('type').value; // to get value in input tag
        let pilots = AC.get('pilots') as FormArray;
        let pilots_length = pilots.length;
        for (let i = 0; i<pilots_length;i++){
            const pilot = pilots.controls[i] as FormGroup;
            if(pilot.controls.birth_date.value){
                const timeDiff = Math.abs(Date.now() - pilot.controls.birth_date.value);
                const age = Math.floor(timeDiff / (1000 * 3600 * 24) / 365);
                if (
                (type === 'Niños' &&
                (age < 5 || age > 12)) ||
                (type === 'Adultos' && age < 12)
                ) {
                    pilot.get('birth_date').setErrors({AgeValidator: true});
                }else{
                    pilot.get('birth_date').setErrors(null);
                }
            }
        }
    }
}


